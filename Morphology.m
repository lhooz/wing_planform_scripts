
%% Inputs
R=0.133333;            % wiing lenth in m
AR=2;                    % single wing aspect ratio
r1_hat=0.6;              % non-dimensinal radius of first moment of wing area
x_LE_hat=0.5;             % non-dimensinal position of the wing leading edge

yr=0.011;           % y dimension of wing root offset in m (along span)
xr=0;           % x dimension of wing root offset in m (along chord)

%% Beta function

c_bar=R/AR;                     % mean geometric chord
n=100;                          % no of points to draw
r2_hat=0.929*(r1_hat^0.732);    % from Ellington statistical relation

p=r1_hat*(((r1_hat*(1-r1_hat))/((r2_hat^2)-(r1_hat^2)))-1);
q=(1-r1_hat)*(((r1_hat*(1-r1_hat))/((r2_hat^2)-(r1_hat^2)))-1);
F = @(x)x.^(p-1).*((1-x).^(q-1));
B = quad(F,0,1);
dr=R/n;

for i=1:(n+1)
    r(i)=(i-1)*dr;
    r_hat(i)=r(i)/R;
    c_hat1(i)=(((r_hat(i))^(p-1))*((1-(r_hat(i)))^(q-1)))/B;
    c(i)=c_hat1(i)*c_bar;
    y_LE(i)=yr+r(i);
    y_TE(i)=yr+r(i);
    x_LE(i)=xr+x_LE_hat*c(i);
    x_TE(i)=xr+(x_LE_hat-1)*c(i);
end

%% r2hat calc
S_nooffset = trapz(r, c) % no offset
S_offset = trapz((r + yr), c) % offset

S1_nooffset = trapz(r, (c.*r))
S1_offset = trapz((r + yr), (c.*(r + yr)))
r1_hat_nooffset = S1_nooffset/(S_nooffset*R)
r1_hat_offset = S1_offset/(S_offset*R)

S2_nooffset = trapz(r, (c.*(r.^2)))
S2_offset = trapz((r + yr), (c.*(((r+yr).^2))))
r2_hat_nooffset = (S2_nooffset/(S_nooffset*(R^2)))^0.5
r2_hat_offset = (S2_offset/(S_offset*((R+yr)^2)))^0.5

%% Plotting
% 
% CMRmap=[0 0 0;0 0.4470 0.7410;0.8500 0.3250 0.0980;0.9290 0.6940 0.1250;0.4940 0.1840 0.5560;0.4660 0.6740 0.1880;0.3010 0.7450 0.9330;0.6350 0.0780 0.1840;1 1 1];
% CMRmap1=[0 0 0;.15 .15 .5;.3 .15 .75;.6 .2 .50;1 .25 .15;.9 .5 0;.9 .75 .1;.9 .9 .5;1 1 1];
% 
% figure
% plot(y_LE,x_LE,'-','LineWidth',2,'Color',CMRmap(2,:),'MarkerEdgeColor',CMRmap(1,:),'MarkerFaceColor',CMRmap(1,:),'MarkerSize', 10)
% hold on
% plot(y_TE,x_TE,'-','LineWidth',2,'Color',CMRmap(2,:),'MarkerEdgeColor',CMRmap(1,:),'MarkerFaceColor',CMRmap(2,:),'MarkerSize', 10)
% 
% % set(gca,'XTick',0:0.5:1,'FontName','Arial','FontSize',40)
% % xlim([0 1])
% % set(gca,'YTick',-1:1:1,'FontName','Arial','FontSize',40)
% % ylim([-1.05 1.05])
% xlabel('y (m)','FontWeight','n','FontAngle','n','FontName','Arial','FontSize',20,'color','k')
% ylabel('x (m)','FontWeight','n','FontAngle','normal','FontName','Arial','FontSize',20,'color','k')
% grid on
% % legend('?','Location','northeast')
% axis equal
% set(gca,'FontSize',20,'FontWeight','n','linewidth',2)
% grid on
% set(gca,'Xcolor',[0.5 0.5 0.5]);
% set(gca,'Ycolor',[0.5 0.5 0.5]);
% Caxes = copyobj(gca,gcf);
% set(Caxes, 'color', 'none', 'xcolor', 'k', 'xgrid', 'off', 'ycolor','k', 'ygrid','off');
% set(gca,'GridLineStyle','--','LineWidth',2)